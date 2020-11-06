import { EventFL } from './../../models/eventsFL';
import { Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class HeaderService {

  httpOptionsI = {
    headers: {
      "X-Session-Token": `${localStorage.getItem("currentUser")}`
    }
  };

  constructor(private http: HttpClient) { }

  getUserImgUrl(): Observable<string>{
    return this.http
    .get<string>('http://localhost:8000/api/user/me/avatar', this.httpOptionsI)
  }

  getImg(url: string): Observable<Blob>{
    return this.http
    .get('http://localhost:8000' + url, {responseType: 'blob'})
  }

  getSerchingEvents(input: string){
    let httpOptionsDefault = {
      headers:{
        "Content-Type": "application/json; charset=utf-8"
      },
      params:{
        'name': input
      }
    }
    return this.http
    .get<EventFL[]>('http://localhost:8000/api/events', httpOptionsDefault)
  }
}
