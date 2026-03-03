"use client"

import { useState, useCallback } from "react"
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

// Demo response generator for the UI prototype
function generateDemoResponse(
  query: string,
  files: UploadedFile[]
): { content: string; sources: Source[] } {
  const fileNames = files.map((f) => f.name)

  const responses = [
    {
      content: `Based on the documents in your knowledge base, here is what I found:\n\n## Key Findings\n\nThe analysis reveals several important points related to your query about **"${query}"**:\n\n1. **Primary Insight** — The documents contain relevant information that directly addresses your question. Multiple sections across different files corroborate this finding.\n\n2. **Supporting Evidence** — Cross-referencing the uploaded materials shows consistent patterns and data points.\n\n3. **Additional Context** — There are related topics in the documents that may provide further depth to your understanding.\n\n### Recommendation\n\nBased on the retrieved context, I suggest reviewing the highlighted sources below for more detailed information. The \`relevant sections\` contain specific data points that support these conclusions.`,
      sources: fileNames.slice(0, 2).map((name, i) => ({
        fileName: name,
        snippet:
          i === 0
            ? "This section discusses the primary findings and methodology used in the analysis, providing a comprehensive overview of the results..."
            : "Supporting data and cross-referenced evidence from secondary analysis confirms the initial hypothesis outlined in the primary document...",
        page: Math.floor(Math.random() * 20) + 1,
      })),
    },
    {
      content: `Great question! After searching through your uploaded documents, here's a summary:\n\n## Summary\n\nYour query about **"${query}"** maps to several key areas:\n\n- **Definition & Scope** — The documents define this concept clearly with supporting examples\n- **Implementation Details** — Step-by-step processes are outlined across multiple files\n- **Best Practices** — Several recommendations are highlighted in the source materials\n\nThe most relevant information comes from the sources listed below. Each source has been ranked by relevance to your specific question.\n\n> *Note: For the most accurate results, ensure all relevant documents have been uploaded to the knowledge base.*`,
      sources: fileNames.slice(0, 3).map((name, i) => ({
        fileName: name,
        snippet: [
          "The document provides a thorough definition and framework for understanding the core concepts discussed in this analysis...",
          "Step-by-step implementation guide covering the essential procedures and workflows for practical application...",
          "Best practices section outlining recommended approaches based on empirical evidence and industry standards...",
        ][i] || "Related content found in document...",
        page: Math.floor(Math.random() * 15) + 1,
      })),
    },
  ]

  if (files.length === 0) {
    return {
      content: `I'd be happy to help answer your question about **"${query}"**, but I notice you haven't uploaded any documents yet.\n\n### Getting Started\n\n1. Use the **sidebar** on the left to upload your documents (.txt, .pdf, .doc)\n2. You can drag and drop files or click the upload area\n3. Once uploaded, ask me anything about their contents\n\nI support the following formats:\n- \`.txt\` — Plain text files\n- \`.pdf\` — PDF documents\n- \`.doc / .docx\` — Microsoft Word documents\n\nUpload some files and let's get started!`,
      sources: [],
    }
  }

  return responses[Math.floor(Math.random() * responses.length)]
}

export function RagChat() {
  const [files, setFiles] = useState<UploadedFile[]>([])
  const [messages, setMessages] = useState<Message[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [sidebarOpen, setSidebarOpen] = useState(true)

  const handleUpload = useCallback((newFiles: File[]) => {
    const uploadedFiles: UploadedFile[] = newFiles.map((f) => ({
      id: crypto.randomUUID(),
      name: f.name,
      size: f.size,
      type: f.type,
      uploadedAt: new Date(),
    }))
    setFiles((prev) => [...prev, ...uploadedFiles])
  }, [])

  const handleDelete = useCallback((id: string) => {
    setFiles((prev) => prev.filter((f) => f.id !== id))
  }, [])

  const handleReset = useCallback(() => {
    setMessages([])
    setFiles([])
    setIsLoading(false)
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

      // Simulate AI response delay
      await new Promise((r) => setTimeout(r, 1200 + Math.random() * 800))

      const { content: responseContent, sources } = generateDemoResponse(
        content,
        files
      )

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
