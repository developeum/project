import { Base64 } from './../../../models/Base64';
import { EventFL } from './../../../models/eventsFL';
import { User } from './../../../models/user';
import { Observable } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { retry } from 'rxjs/operators';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class PersonalService {
  httpOptions = {
    headers:{
      Authorization: "Bearer" + localStorage.getItem("currentUser")
    }
  }

  constructor(private http:HttpClient) { }

  getUserInfo(): Observable<User>{
    return this.http
    .get<User>("http://localhost:8000/api/user/me", this.httpOptions)
    .pipe(retry(1))
  }

  getFavEvents(): Observable<EventFL[]>{
    return this.http
    .get<EventFL[]>("http://localhost:8000/api/user/me/favorites", this.httpOptions)
    .pipe(retry(1))
  }

  getPicBase64(){
    return this.http
    .get<Base64>("http://localhost:8000/api/user/me/avatar", this.httpOptions)
    .pipe(retry(1))
  }
}
