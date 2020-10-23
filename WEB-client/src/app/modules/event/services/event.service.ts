import { retry } from 'rxjs/operators';
import { Event } from './../../../models/event';
import { Observable } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class EventService {
  httpOptions = {
    headers: new HttpHeaders({
      "Content-Type": "application/json; charset=utf-8"
    })
  };

  httpUserOptions = {
    headers: {
      Authentication: "Bearer" + localStorage.getItem("currentUser")
    }
  }

  constructor(private http: HttpClient) { }

  getEventData(id: number): Observable<Event>{
    return this.http
    .get<Event>("http://localhost:8000/api/events/" + id, this.httpOptions)
    .pipe(retry(1))
  }

  postToVisited(data: number){
    return this.http
    .post("http://localhost:8000/api/user/me/visited", {
      id: data
    },
    this.httpUserOptions
    )
    .pipe(retry(1))
  }

  getEventImg(imageUrl: string): Observable<Blob>{
    return this.http.get(imageUrl, {responseType: 'blob'})
  }

  
}
