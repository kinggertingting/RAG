"use client"

import { useState, useRef, useCallback } from "react"
import {
  Upload,
  FileText,
  FileType,
  File,
  Trash2,
  X,
  PanelLeftClose,
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Badge } from "@/components/ui/badge"
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip"
import { cn } from "@/lib/utils"
import type { UploadedFile } from "@/lib/types"

const ACCEPTED_TYPES: Record<string, string> = {
  "text/plain": ".txt",
  "application/pdf": ".pdf",
  "application/msword": ".doc",
  "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
    ".docx",
}

const ACCEPTED_EXTENSIONS = [".txt", ".pdf", ".doc", ".docx"]

function getFileIcon(name: string) {
  const ext = name.split(".").pop()?.toLowerCase()
  if (ext === "pdf") return <FileType className="size-4 shrink-0 text-destructive" />
  if (ext === "doc" || ext === "docx")
    return <FileText className="size-4 shrink-0 text-primary" />
  return <File className="size-4 shrink-0 text-muted-foreground" />
}

function formatSize(bytes: number) {
  if (bytes < 1024) return `${bytes} B`
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
}

interface FileSidebarProps {
  files: UploadedFile[]
  onUpload: (files: File[]) => void
  onDelete: (id: string) => void
  open: boolean
  onClose: () => void
}

export function FileSidebar({
  files,
  onUpload,
  onDelete,
  open,
  onClose,
}: FileSidebarProps) {
  const [isDragging, setIsDragging] = useState(false)
  const inputRef = useRef<HTMLInputElement>(null)
  const dragCounter = useRef(0)

  const handleFiles = useCallback(
    (fileList: FileList | null) => {
      if (!fileList) return
      const valid = Array.from(fileList).filter((f) => {
        const ext = "." + f.name.split(".").pop()?.toLowerCase()
        return (
          Object.keys(ACCEPTED_TYPES).includes(f.type) ||
          ACCEPTED_EXTENSIONS.includes(ext)
        )
      })
      if (valid.length > 0) onUpload(valid)
    },
    [onUpload]
  )

  const onDragEnter = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    dragCounter.current++
    setIsDragging(true)
  }, [])

  const onDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    dragCounter.current--
    if (dragCounter.current === 0) setIsDragging(false)
  }, [])

  const onDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
  }, [])

  const onDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault()
      e.stopPropagation()
      dragCounter.current = 0
      setIsDragging(false)
      handleFiles(e.dataTransfer.files)
    },
    [handleFiles]
  )

  return (
    <aside
      className={cn(
        "flex h-full w-72 shrink-0 flex-col border-r border-border bg-sidebar transition-all duration-300 lg:relative",
        "fixed inset-y-0 left-0 z-40",
        open ? "translate-x-0" : "-translate-x-full lg:translate-x-0 lg:w-72",
        !open && "lg:w-0 lg:border-r-0 lg:overflow-hidden"
      )}
    >
      {/* Header */}
      <div className="flex items-center justify-between border-b border-sidebar-border px-4 py-3">
        <div className="flex items-center gap-2">
          <Upload className="size-4 text-primary" />
          <h2 className="text-sm font-semibold text-sidebar-foreground">
            Documents
          </h2>
          {files.length > 0 && (
            <Badge variant="secondary" className="text-[10px] px-1.5 py-0">
              {files.length}
            </Badge>
          )}
        </div>
        <Button
          variant="ghost"
          size="icon-sm"
          onClick={onClose}
          className="text-muted-foreground hover:text-foreground"
          aria-label="Close sidebar"
        >
          <PanelLeftClose className="size-4" />
        </Button>
      </div>

      {/* Drop zone */}
      <div className="px-3 pt-3">
        <div
          onDragEnter={onDragEnter}
          onDragLeave={onDragLeave}
          onDragOver={onDragOver}
          onDrop={onDrop}
          onClick={() => inputRef.current?.click()}
          role="button"
          tabIndex={0}
          onKeyDown={(e) => {
            if (e.key === "Enter" || e.key === " ") inputRef.current?.click()
          }}
          aria-label="Upload files"
          className={cn(
            "flex cursor-pointer flex-col items-center justify-center gap-2 rounded-lg border-2 border-dashed px-4 py-6 transition-colors",
            isDragging
              ? "border-primary bg-primary/10 text-primary"
              : "border-border text-muted-foreground hover:border-primary/50 hover:bg-accent/50"
          )}
        >
          <div
            className={cn(
              "flex size-10 items-center justify-center rounded-full transition-colors",
              isDragging ? "bg-primary/20" : "bg-muted"
            )}
          >
            <Upload className="size-5" />
          </div>
          <div className="text-center">
            <p className="text-xs font-medium">
              {isDragging ? "Drop files here" : "Drop files or click to upload"}
            </p>
            <p className="mt-0.5 text-[10px] text-muted-foreground">
              .txt, .pdf, .doc, .docx
            </p>
          </div>
          <input
            ref={inputRef}
            type="file"
            multiple
            accept=".txt,.pdf,.doc,.docx"
            className="hidden"
            onChange={(e) => {
              handleFiles(e.target.files)
              e.target.value = ""
            }}
          />
        </div>
      </div>

      {/* File list */}
      <ScrollArea className="flex-1 px-3 py-2">
        {files.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-12 text-center">
            <FileText className="size-8 text-muted-foreground/40" />
            <p className="mt-2 text-xs text-muted-foreground">
              No documents yet
            </p>
          </div>
        ) : (
          <div className="flex flex-col gap-1">
            {files.map((file) => (
              <div
                key={file.id}
                className="group flex items-center gap-2.5 rounded-md px-2.5 py-2 transition-colors hover:bg-sidebar-accent"
              >
                {getFileIcon(file.name)}
                <div className="min-w-0 flex-1">
                  <Tooltip>
                    <TooltipTrigger asChild>
                      <p className="truncate text-xs font-medium text-sidebar-foreground">
                        {file.name}
                      </p>
                    </TooltipTrigger>
                    <TooltipContent side="right">{file.name}</TooltipContent>
                  </Tooltip>
                  <p className="text-[10px] text-muted-foreground">
                    {formatSize(file.size)}
                  </p>
                </div>
                <Button
                  variant="ghost"
                  size="icon-sm"
                  onClick={() => onDelete(file.id)}
                  className="size-6 opacity-0 transition-opacity group-hover:opacity-100 text-muted-foreground hover:text-destructive"
                  aria-label={`Delete ${file.name}`}
                >
                  <Trash2 className="size-3.5" />
                </Button>
              </div>
            ))}
          </div>
        )}
      </ScrollArea>
    </aside>
  )
}
