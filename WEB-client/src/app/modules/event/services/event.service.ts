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
      "X-Session-Token": `${localStorage.getItem('currentUser')}`,
    }
  }

  constructor(private http: HttpClient) { }

  getEventData(id: number): Observable<Event>{
    return this.http
    .get<Event>("http://localhost:8000/api/events/" + id, this.httpOptions)
    .pipe(retry(1))
  }

  postToVisited(data: number, type: string){
    return this.http
    .post("http://localhost:8000/api/user/me/visited", {
      event_id: Number(data),
      type: type
    },
    this.httpUserOptions
    )
    .pipe(retry(1))
    .subscribe(x => {
      console.log(x)
    })
  }

  getEventImg(imageUrl: string): Observable<Blob>{
    return this.http.get(imageUrl, {responseType: 'blob'})
  }

  
}
