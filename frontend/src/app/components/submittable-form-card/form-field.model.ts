
export interface FormField {
  name: string;
  initialvalue: string;
  validators?: Validators[];
}

interface Validators {
  name: string;
  value?: number;
}
