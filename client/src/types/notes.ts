// ISO 8601 timestamp type
export type Timestamp = string;

export interface Note {
  id: string;
  content: string;
  user_id: string;
  created_at: Timestamp;
  updated_at: Timestamp;
  metadata: NoteMetadata;
}

export interface NoteCreate {
  content: string;
  user_id: string;
}

export interface NoteUpdate {
  content?: string;
  metadata?: NoteMetadata;
}

export interface NoteEnrichment {
  summary: string;
  topics: string[];
  sentiment: string;
  key_entities: string[];
  suggested_tags: string[];
  complexity_score: number;
  enrichment_timestamp: Timestamp;
  llm_model: string;
}

export interface NoteMetadata {
  summary?: string;
  topics?: string[];
  sentiment?: string;
  key_entities?: string[];
  suggested_tags?: string[];
  complexity_score?: number;
  enrichment_timestamp?: Timestamp;
  llm_model?: string;
}

export interface CreateNoteFormData {
  content: string;
}

export interface NoteCreate {
  content: string;
  user_id: string;
}

export interface NoteUpdate {
  content?: string;
  metadata?: NoteMetadata;
}

export interface NoteEnrichment {
  summary: string;
  topics: string[];
  sentiment: string;
  key_entities: string[];
  suggested_tags: string[];
  complexity_score: number;
  enrichment_timestamp: string;
  llm_model: string;
}

export interface NoteMetadata {
  summary?: string;
  topics?: string[];
  sentiment?: string;
  key_entities?: string[];
  suggested_tags?: string[];
  complexity_score?: number;
  enrichment_timestamp?: string;
  llm_model?: string;
}

export interface CreateNoteFormData {
  content: string;
}
