export interface UploadedFile {
  id: string
  name: string
  size: number
}

export interface Source {
  fileName: string
  snippet: string
  page?: number
}

export interface Message {
  id: string
  role: "user" | "assistant"
  content: string
  sources?: Source[]
  createdAt: Date
}
