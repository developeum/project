import { Stack } from './../../../models/stack';
import { Type } from './../../../models/types';
import { Observable } from 'rxjs';
import { EventFL } from './../../../models/eventsFL';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { retry } from 'rxjs/operators';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class EventsService {
  httpOptions = {
    headers: new HttpHeaders({
      "Content-Type": "application/json; charset=utf-8"
    })
  }

  constructor(private http: HttpClient) { }

  getEvents(): Observable<EventFL[]>{
    return this.http
    .get<EventFL[]>("http://localhost:8000/api/events", this.httpOptions)
    .pipe(retry(1))
  }

  getRec(id: string): Observable<EventFL[]>{
    return this.http
    .get<EventFL[]>("http://localhost:8000/api/events/recomended", this.httpOptions)
    .pipe(retry(1))
  }

  getTypes(): Observable<Type[]>{
    return this.http
    .get<Type[]>("http://localhost:8000/api/general/event_types", this.httpOptions)
    .pipe(retry(1))
  }

  getStack(): Observable<Stack[]>{
    return this.http
    .get<Stack[]>("http://localhost:8000/api/general/categories", this.httpOptions)
    .pipe(retry(1))
  }
}
