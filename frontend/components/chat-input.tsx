"use client"

import { useState, useRef, useEffect } from "react"
import { SendHorizontal, Loader2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"

interface ChatInputProps {
  onSend: (message: string) => void
  isLoading: boolean
  disabled?: boolean
}

export function ChatInput({ onSend, isLoading, disabled }: ChatInputProps) {
  const [value, setValue] = useState("")
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto"
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 200)}px`
    }
  }, [value])

  const handleSubmit = () => {
    const trimmed = value.trim()
    if (!trimmed || isLoading) return
    onSend(trimmed)
    setValue("")
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto"
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      handleSubmit()
    }
  }

  const canSend = value.trim().length > 0 && !isLoading && !disabled

  return (
    <div className="shrink-0 border-t border-border bg-background px-4 py-3">
      <div className="mx-auto flex max-w-3xl items-end gap-2">
        <div className="relative flex-1">
          <textarea
            ref={textareaRef}
            value={value}
            onChange={(e) => setValue(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask a question about your documents..."
            disabled={isLoading || disabled}
            rows={1}
            className={cn(
              "flex w-full resize-none rounded-xl border border-input bg-card px-4 py-3 pr-12 text-sm leading-relaxed",
              "placeholder:text-muted-foreground",
              "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring/50 focus-visible:border-ring",
              "disabled:cursor-not-allowed disabled:opacity-50",
              "min-h-[48px] max-h-[200px] text-foreground"
            )}
          />
          <Button
            type="button"
            size="icon-sm"
            onClick={handleSubmit}
            disabled={!canSend}
            className={cn(
              "absolute right-2 bottom-2 rounded-lg transition-all",
              canSend
                ? "bg-primary text-primary-foreground shadow-sm hover:bg-primary/90"
                : "bg-muted text-muted-foreground"
            )}
            aria-label="Send message"
          >
            {isLoading ? (
              <Loader2 className="size-4 animate-spin" />
            ) : (
              <SendHorizontal className="size-4" />
            )}
          </Button>
        </div>
      </div>
      <p className="mx-auto mt-1.5 max-w-3xl text-center text-[10px] text-muted-foreground">
        {"Press Enter to send, Shift+Enter for new line"}
      </p>
    </div>
  )
}
