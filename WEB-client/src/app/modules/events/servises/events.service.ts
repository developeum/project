import { City } from './../../../models/city';
import { Stack } from './../../../models/stack';
import { Type } from './../../../models/types';
import { Observable } from 'rxjs';
import { EventFL } from './../../../models/eventsFL';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { retry } from 'rxjs/operators';
import { Injectable } from '@angular/core';
import * as jwt_decode from "jwt-decode";

@Injectable({
  providedIn: 'root'
})
export class EventsService {
  userId: number;

  httpOptions = {
    headers: new HttpHeaders({
      "Content-Type": "application/json; charset=utf-8"
    })
  }

  

  constructor(private http: HttpClient) { 
    
  }

  getEvents(type: [number], stack: [number], city: [number], starts_at_min: string, starts_at_max: string){
    if (localStorage.getItem("currentUser") != null) {
      let headers = new HttpHeaders();
      headers.append('Authorization', 'Bearer' + localStorage.getItem('currentUser'))
      let httpParams = new HttpParams()
      .set('types', type.toString())
      .set('categories', stack.toString())
      .set('cities', city.toString())
      .set('starts_at_min', starts_at_min)
      .set('starts_at_max', starts_at_max)
      let options = {headers, httpParams}
      return this.http
        .get<EventFL[]>("http://localhost:8000/api/events", options)
        .pipe(retry(1))
    } else {
      let headers = new HttpHeaders({"Content-Type": "application/json; charset=utf-8"})
      let httpParams = new HttpParams()
      .set('types', type.toString())
      .set('categories', stack.toString())
      .set('cities', city.toString())
      .set('starts_at_min', starts_at_min)
      .set('starts_at_max', starts_at_max);
      let options = {headers, httpParams}
      return this.http
        .get<EventFL[]>("http://localhost:8000/api/events", options)
        .pipe(retry(1))
    }
  }

  getClearEvents(): Observable<EventFL[]>{
    return this.http
    .get<EventFL[]>('http://localhost:8000/api/events', this.httpOptions)
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

  getCities(): Observable<City[]>{
    return this.http
    .get<City[]>("http://localhost:8000/api/general/cities", this.httpOptions)
    .pipe(retry(1))
  }
}
