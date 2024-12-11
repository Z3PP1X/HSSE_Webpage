import { Choices } from "./choices.interface";

export interface QuestionMetadata {
  key: string;
  label: string;
  value: string;
  required: boolean;
  controlType: string;
  type: string;
  order: number;
  options: Choices[];
}
