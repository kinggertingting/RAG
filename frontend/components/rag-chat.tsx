"use client"

import { useState, useCallback, useEffect } from "react"
import { PanelLeft, RotateCcw } from "lucide-react"
import { Button } from "@/components/ui/button"
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog"
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip"
import { ThemeToggle } from "@/components/theme-toggle"
import { FileSidebar } from "@/components/file-sidebar"
import { ChatMessages } from "@/components/chat-messages"
import { ChatInput } from "@/components/chat-input"
import type { UploadedFile, Message, Source } from "@/lib/types"
import { getAllFiles, deleteAllFiles } from "@/lib/api"
import { query } from "@/lib/api"
import { tr } from "date-fns/locale"

export function RagChat() {
  const [files, setFiles] = useState<UploadedFile[]>([])
  const [messages, setMessages] = useState<Message[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [sidebarOpen, setSidebarOpen] = useState(true)

  useEffect(() => {
    async function loadFiles() {
      try {
        const data = await getAllFiles()

        const files: UploadedFile[] = data.files.map((f: any) => ({
          id: f.file_id,
          name: f.file_name,
          size: 0,
          type: "",
          uploadedAt: new Date()
        }))

        setFiles(files)

      } catch (err) {
        console.error("Load files error:", err)
      }
    }

    loadFiles()
  }, [])

  const handleUpload = useCallback((uploadedFiles: UploadedFile[]) => {
    setFiles((prev) => [...prev, ...uploadedFiles])
  }, [])

  const handleDelete = useCallback((id: string) => {
    setFiles((prev) => prev.filter((f) => f.id !== id))
  }, [])

  const handleReset = useCallback(async () => {
    try {
      await deleteAllFiles()
      setMessages([])
      setFiles([])
      setIsLoading(false)
    } catch (err) {
      console.error("Reset error:", err)
    }
  }, [])

  const handleSend = useCallback(
    async (content: string) => {
      const userMessage: Message = {
        id: crypto.randomUUID(),
        role: "user",
        content,
        createdAt: new Date(),
      }

      setMessages((prev) => [...prev, userMessage])
      setIsLoading(true)

      const result = await query(content)

      const responseContent = result.answer

      const sources =
        result.contexts?.map((ctx: any) => ({
          fileName: ctx.file_name,
          snippet: ctx.text?.slice(0, 200) || "",
          page: ctx.chunk_index,
        })) || []

      const assistantMessage: Message = {
        id: crypto.randomUUID(),
        role: "assistant",
        content: responseContent,
        sources,
        createdAt: new Date(),
      }

      setMessages((prev) => [...prev, assistantMessage])
      setIsLoading(false)
    },
    [files]


  )

  return (
    <div className="flex h-dvh overflow-hidden bg-background">
      {/* Mobile backdrop */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 z-30 bg-background/80 backdrop-blur-sm lg:hidden"
          onClick={() => setSidebarOpen(false)}
          aria-hidden="true"
        />
      )}

      {/* Sidebar */}
      <FileSidebar
        files={files}
        onUpload={handleUpload}
        onDelete={handleDelete}
        open={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
      />

      {/* Main Chat Area */}
      <main className="flex min-h-0 min-w-0 flex-1 flex-col overflow-hidden">
        {/* Top bar */}
        <header className="flex shrink-0 items-center justify-between border-b border-border px-4 py-2.5">
          <div className="flex items-center gap-2">
            {!sidebarOpen && (
              <Button
                variant="ghost"
                size="icon-sm"
                onClick={() => setSidebarOpen(true)}
                className="text-muted-foreground hover:text-foreground"
                aria-label="Open sidebar"
              >
                <PanelLeft className="size-4" />
              </Button>
            )}
            <div className="flex items-center gap-2">
              <div className="flex size-6 items-center justify-center rounded-md bg-primary text-primary-foreground">
                <svg
                  className="size-3.5"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2.5"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <path d="m21.44 11.05-9.19 9.19a6 6 0 0 1-8.49-8.49l8.57-8.57A4 4 0 1 1 18 8.84l-8.59 8.57a2 2 0 0 1-2.83-2.83l8.49-8.48" />
                </svg>
              </div>
              <h1 className="text-sm font-semibold text-foreground">
                RAG Chat
              </h1>
            </div>
          </div>
          <div className="flex items-center gap-1">
            {/* Reset button */}
            <AlertDialog>
              <Tooltip>
                <TooltipTrigger asChild>
                  <AlertDialogTrigger asChild>
                    <Button
                      variant="ghost"
                      size="icon-sm"
                      className="text-muted-foreground hover:text-foreground"
                      aria-label="Reset conversation"
                    >
                      <RotateCcw className="size-4" />
                    </Button>
                  </AlertDialogTrigger>
                </TooltipTrigger>
                <TooltipContent>Reset session</TooltipContent>
              </Tooltip>
              <AlertDialogContent>
                <AlertDialogHeader>
                  <AlertDialogTitle>Reset session?</AlertDialogTitle>
                  <AlertDialogDescription>
                    This will clear all messages and uploaded files. This action
                    cannot be undone and the current session will not be saved.
                  </AlertDialogDescription>
                </AlertDialogHeader>
                <AlertDialogFooter>
                  <AlertDialogCancel>Cancel</AlertDialogCancel>
                  <AlertDialogAction
                    onClick={handleReset}
                    className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
                  >
                    Reset
                  </AlertDialogAction>
                </AlertDialogFooter>
              </AlertDialogContent>
            </AlertDialog>
            <ThemeToggle />
          </div>
        </header>

        {/* Messages - only this area scrolls */}
        <ChatMessages messages={messages} isLoading={isLoading} />

        {/* Input - pinned to bottom */}
        <ChatInput onSend={handleSend} isLoading={isLoading} />
      </main>
    </div>
  )
}
