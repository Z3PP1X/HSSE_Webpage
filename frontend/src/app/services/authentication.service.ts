import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Observable } from 'rxjs';


@Injectable({
  providedIn: 'root'
})
export class AuthenticationService {

  constructor (private http: HttpClient){}

    email = "user5@example.com"
    pass = "Testpass123"

    requestURL = "http://127.0.0.1:8000/api/user/token/?format=json"



}
