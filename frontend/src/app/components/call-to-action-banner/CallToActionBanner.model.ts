export interface CallToActionBanner {
    id: number; 
    content: Content[];
}

interface Content{
    id: number; 
    h1: string;
    h2: string;
    text: string;
    smalltext: string; 

}