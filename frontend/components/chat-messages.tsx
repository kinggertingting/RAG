"use client"

import { useRef, useEffect } from "react"
import { Bot, User, FileText, BookOpen } from "lucide-react"
import { ScrollArea } from "@/components/ui/scroll-area"
import { cn } from "@/lib/utils"
import type { Message, Source } from "@/lib/types"
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover"

function renderMarkdown(content: string) {
  const lines = content.split("\n")
  const elements: React.ReactNode[] = []
  let i = 0

  while (i < lines.length) {
    const line = lines[i]

    // Code block
    if (line.startsWith("```")) {
      const lang = line.slice(3).trim()
      const codeLines: string[] = []
      i++
      while (i < lines.length && !lines[i].startsWith("```")) {
        codeLines.push(lines[i])
        i++
      }
      i++ // skip closing ```
      elements.push(
        <pre
          key={`code-${i}`}
          className="my-2 overflow-x-auto rounded-lg bg-muted/80 p-3 text-xs leading-relaxed"
        >
          <code className="font-mono text-foreground">
            {codeLines.join("\n")}
          </code>
        </pre>
      )
      continue
    }

    // Heading
    if (line.startsWith("### ")) {
      elements.push(
        <h3 key={`h3-${i}`} className="mt-3 mb-1 text-sm font-semibold text-foreground">
          {renderInline(line.slice(4))}
        </h3>
      )
    } else if (line.startsWith("## ")) {
      elements.push(
        <h2 key={`h2-${i}`} className="mt-4 mb-1 text-base font-bold text-foreground">
          {renderInline(line.slice(3))}
        </h2>
      )
    } else if (line.startsWith("# ")) {
      elements.push(
        <h1 key={`h1-${i}`} className="mt-4 mb-2 text-lg font-bold text-foreground">
          {renderInline(line.slice(2))}
        </h1>
      )
    }
    // Unordered list
    else if (line.match(/^[-*]\s/)) {
      const items: string[] = [line.replace(/^[-*]\s/, "")]
      while (i + 1 < lines.length && lines[i + 1].match(/^[-*]\s/)) {
        i++
        items.push(lines[i].replace(/^[-*]\s/, ""))
      }
      elements.push(
        <ul key={`ul-${i}`} className="my-1.5 ml-4 list-disc space-y-0.5 text-sm leading-relaxed">
          {items.map((item, idx) => (
            <li key={idx}>{renderInline(item)}</li>
          ))}
        </ul>
      )
    }
    // Ordered list
    else if (line.match(/^\d+\.\s/)) {
      const items: string[] = [line.replace(/^\d+\.\s/, "")]
      while (i + 1 < lines.length && lines[i + 1].match(/^\d+\.\s/)) {
        i++
        items.push(lines[i].replace(/^\d+\.\s/, ""))
      }
      elements.push(
        <ol key={`ol-${i}`} className="my-1.5 ml-4 list-decimal space-y-0.5 text-sm leading-relaxed">
          {items.map((item, idx) => (
            <li key={idx}>{renderInline(item)}</li>
          ))}
        </ol>
      )
    }
    // Empty line
    else if (line.trim() === "") {
      elements.push(<div key={`br-${i}`} className="h-2" />)
    }
    // Regular paragraph
    else {
      elements.push(
        <p key={`p-${i}`} className="text-sm leading-relaxed">
          {renderInline(line)}
        </p>
      )
    }

    i++
  }

  return elements
}

function renderInline(text: string) {
  // Handle inline code, bold, italic
  const parts: React.ReactNode[] = []
  const regex = /(`[^`]+`|\*\*[^*]+\*\*|\*[^*]+\*)/g
  let lastIndex = 0
  let match

  while ((match = regex.exec(text)) !== null) {
    if (match.index > lastIndex) {
      parts.push(text.slice(lastIndex, match.index))
    }

    const token = match[0]
    if (token.startsWith("`") && token.endsWith("`")) {
      parts.push(
        <code
          key={match.index}
          className="rounded bg-muted px-1 py-0.5 font-mono text-xs text-primary"
        >
          {token.slice(1, -1)}
        </code>
      )
    } else if (token.startsWith("**") && token.endsWith("**")) {
      parts.push(
        <strong key={match.index} className="font-semibold">
          {token.slice(2, -2)}
        </strong>
      )
    } else if (token.startsWith("*") && token.endsWith("*")) {
      parts.push(<em key={match.index}>{token.slice(1, -1)}</em>)
    }

    lastIndex = match.index + token.length
  }

  if (lastIndex < text.length) {
    parts.push(text.slice(lastIndex))
  }

  return parts.length > 0 ? parts : text
}

function SourceCard({ source }: { source: Source }) {
  return (
    <Popover>
      <PopoverTrigger asChild>
        <div className="cursor-pointer flex items-start gap-2 rounded-lg border border-primary/20 bg-primary/5 px-3 py-2 transition-colors hover:bg-primary/10">
          <FileText className="mt-0.5 size-3.5 shrink-0 text-primary" />
          <div className="min-w-0 flex-1">
            <p className="truncate text-xs font-medium text-primary">
              {source.fileName}
              {source.page && (
                <span className="ml-1 text-muted-foreground">
                  {"p." + source.page}
                </span>
              )}
            </p>
            <p className="mt-0.5 line-clamp-2 text-[11px] leading-relaxed text-muted-foreground">
              {source.snippet}
            </p>
          </div>
        </div>
      </PopoverTrigger>

      <PopoverContent className="max-w-md">
        <div className="space-y-2 text-xs">
          <p className="font-semibold text-primary">
            {source.fileName} {source.page && `(chunk ${source.page})`}
          </p>

          <p className="text-muted-foreground leading-relaxed">
            {source.snippet}
          </p>
        </div>
      </PopoverContent>
    </Popover>
  )
}

interface ChatMessagesProps {
  messages: Message[]
  isLoading: boolean
}

export function ChatMessages({ messages, isLoading }: ChatMessagesProps) {
  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages, isLoading])

  if (messages.length === 0 && !isLoading) {
    return (
      <div className="flex flex-1 flex-col items-center justify-center px-4">
        <div className="flex size-16 items-center justify-center rounded-2xl bg-primary/10">
          <BookOpen className="size-8 text-primary" />
        </div>
        <h2 className="mt-4 text-lg font-semibold text-foreground text-balance text-center">
          Ask your documents anything
        </h2>
        <p className="mt-1.5 max-w-sm text-center text-sm text-muted-foreground leading-relaxed">
          Upload documents in the sidebar, then ask questions. The AI will find
          relevant answers from your files.
        </p>
        <div className="mt-6 flex flex-wrap justify-center gap-2">
          {[
            "Summarize the key points",
            "What are the main findings?",
            "Compare the documents",
          ].map((q) => (
            <span
              key={q}
              className="rounded-full border border-border bg-card px-3 py-1.5 text-xs text-muted-foreground"
            >
              {q}
            </span>
          ))}
        </div>
      </div>
    )
  }

  return (
    <ScrollArea className="min-h-0 flex-1">
      <div className="mx-auto max-w-3xl px-4 py-6">
        <div className="flex flex-col gap-6">
          {messages.map((msg) => (
            <div key={msg.id} className="flex gap-3">
              <div
                className={cn(
                  "flex size-7 shrink-0 items-center justify-center rounded-lg",
                  msg.role === "assistant"
                    ? "bg-primary/15 text-primary"
                    : "bg-muted text-muted-foreground"
                )}
              >
                {msg.role === "assistant" ? (
                  <Bot className="size-4" />
                ) : (
                  <User className="size-4" />
                )}
              </div>
              <div className="min-w-0 flex-1 pt-0.5">
                <p className="mb-1 text-xs font-medium text-muted-foreground">
                  {msg.role === "assistant" ? "AI Assistant" : "You"}
                </p>
                <div className="prose-sm text-foreground">
                  {renderMarkdown(msg.content)}
                </div>

                {/* Sources */}
                {msg.sources && msg.sources.length > 0 && (
                  <div className="mt-3">
                    <p className="mb-1.5 flex items-center gap-1 text-[11px] font-medium uppercase tracking-wider text-muted-foreground">
                      <FileText className="size-3" />
                      Sources
                    </p>
                    <div className="grid gap-1.5 sm:grid-cols-2">
                      {msg.sources.map((src, idx) => (
                        <SourceCard key={idx} source={src} />
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          ))}

          {/* Loading indicator */}
          {isLoading && (
            <div className="flex gap-3">
              <div className="flex size-7 shrink-0 items-center justify-center rounded-lg bg-primary/15 text-primary">
                <Bot className="size-4" />
              </div>
              <div className="flex items-center gap-1.5 pt-1">
                <div className="size-1.5 animate-pulse rounded-full bg-primary/60" />
                <div className="size-1.5 animate-pulse rounded-full bg-primary/60 [animation-delay:150ms]" />
                <div className="size-1.5 animate-pulse rounded-full bg-primary/60 [animation-delay:300ms]" />
              </div>
            </div>
          )}
        </div>
        <div ref={bottomRef} />
      </div>
    </ScrollArea>
  )
}
