export interface SubmittableForm {

  id: number; 
  cat: string; 
  questions: QuestionSet[];
  
  }
  
  interface QuestionSet {
    sys_id: string; 
    text: string; 
  }


  