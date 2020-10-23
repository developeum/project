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
  httpOptionsUser = {
    headers:{
      Authorization: "Bearer" + localStorage.getItem("currentUser")
    }
  };

  httpOptionsDefault = {
    headers: new HttpHeaders({
      "Content-Type": "application/json; charset=utf-8"
    })
  };

  constructor(private http:HttpClient) { }

  getUserInfo(): Observable<User>{
    return this.http
    .get<User>("http://localhost:8000/api/user/me", this.httpOptionsUser)
    .pipe(retry(1))
  }

  getFavEvents(): Observable<EventFL[]>{
    return this.http
    .get<EventFL[]>("http://localhost:8000/api/user/me/visited", this.httpOptionsUser)
    .pipe(retry(1))
  }

  getPicBase64(){
    return this.http
    .get<Base64>("http://localhost:8000/api/user/me/avatar", this.httpOptionsUser)
    .pipe(retry(1))
  }

  getStacks(){
    return this.http
    .get("http://localhost:8000/api/general/stacks", this.httpOptionsDefault)
    .pipe(retry(1))
  }

  postInfo(info: User){
    return this.http
    .post("http://localhost:8000/api/user/me",{
      phone: info.phone,
      first_name: info.first_name,
      last_name: info.last_name,
      status: info.status,
      city: info.city,
      stack: info.stack
    })
    
  }
}
