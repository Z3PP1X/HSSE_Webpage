export interface FormConfig {

  id: number;
  title: string;
  category: CategorySet[];
  }

  interface CategorySet{
    id: number;
    name: string;
    questions: QuestionSet[];
  }

  interface QuestionSet {
    sys_id: string;
    label: string;
    validators: QuestionValidators[];
  }

  interface QuestionValidators{
    required: boolean;
    maxCharacters?: number;
    DateTime?: boolean;
    enumerator?: number;

    }



