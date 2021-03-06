import { City } from './../../../models/city';
import { Stack } from './../../../models/stack';
import { Type } from './../../../models/types';
import { Observable } from 'rxjs';
import { EventFL } from './../../../models/eventsFL';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { retry } from 'rxjs/operators';
import { Injectable } from '@angular/core';

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

  getEvents(skip?: number, type: number[] = [], stack: number[] = [], city: number[] = [], starts_at_min: string = "", starts_at_max: string = ""){
    if (localStorage.getItem("currentUser") != null) {
      let httpOptionsUser = {
        headers:{
          "Content-Type": "application/json",
          "X-Session-Token": `${localStorage.getItem("currentUser")}`
        },
        params:{
          'type': type.toString(),
          'category': stack.toString(),
          'city': city.toString(),
          'starts_at_min': starts_at_min,
          'starts_at_max': starts_at_max,
          'skip': skip.toString(),
        }
      };
      return this.http
        .get<EventFL[]>("/api/events", httpOptionsUser)
        .pipe(retry(1))
    } else {
      let httpOption = {
        headers:{
          "Content-Type": "application/json",
        },
        params:{
          'type': type.toString(),
          'category': stack.toString(),
          'city': city.toString(),
          'starts_at_min': starts_at_min,
          'starts_at_max': starts_at_max,
          'skip': skip.toString(),
        }
      };
      return this.http
        .get<EventFL[]>("/api/events", httpOption)
        .pipe(retry(1))
    }
  }

  getClearEvents(): Observable<EventFL[]>{
    return this.http
    .get<EventFL[]>('/api/events', this.httpOptions)
    .pipe(retry(1))
  }

  getTypes(): Observable<Type[]>{
    return this.http
    .get<Type[]>("/api/general/event_types", this.httpOptions)
    .pipe(retry(1))
  }

  getStack(): Observable<Stack[]>{
    return this.http
    .get<Stack[]>("/api/general/categories", this.httpOptions)
    .pipe(retry(1))
  }

  getCities(): Observable<City[]>{
    return this.http
    .get<City[]>("/api/general/cities", this.httpOptions)
    .pipe(retry(1))
  }
}
