import { APIMetadata } from '../interfaces/api-metadata.interface';
import { HttpClient } from "@angular/common/http";
import { Injectable, inject} from "@angular/core";

import { map, tap} from 'rxjs/operators';
import { Observable, of } from "rxjs";
import { MetadataTransformationService } from "./metadata-transformation.service";

"http://127.0.0.1:8000/api/digitalfirstaid/meta/?format=json"

@Injectable({
  providedIn: "root"
})
export class MetadataService{

  private readonly http = inject(HttpClient);
  questionset = inject(MetadataTransformationService)

  private fetchMetadata(url: string){
   return this.http.get<APIMetadata[]>(url).pipe();

  }

  getMetadata(url: string) {
    return this.fetchMetadata(url).pipe(
      map((resData) => this.questionset.convertMetadatatoQuestionModel(resData))

    );
  }





        }



