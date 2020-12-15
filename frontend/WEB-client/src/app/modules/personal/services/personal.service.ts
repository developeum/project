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
  getToken(){
    return localStorage.getItem('currentUser')
  }

  httpOptionsUserImg = {
    headers:{
      "Content-Type": "multipart/form-data",
      "X-Session-Token": `${localStorage.getItem("currentUser")}`
    }
  };

  httpOptionsI = {
    headers: {
      "X-Session-Token": `${localStorage.getItem("currentUser")}`
    }
  }

  httpOptionsUser = {
    headers:{
      "Content-Type": "application/json; charset=utf-8",
      "X-Session-Token": `${localStorage.getItem("currentUser")}`
    }
  };

  httpOptionsDefault = {
    headers: new HttpHeaders({
      "Content-Type": "application/json; charset=utf-8"
    })
  };

  httpPhotoOptions = {
    headers: new HttpHeaders({
      "Content-Type": "multipart/form-data"
    })
  }

  constructor(private http:HttpClient) { }

  getUserInfo(): Observable<User>{
    return this.http
    .get<User>("/api/user/me", this.httpOptionsUser)
    .pipe(retry(1))
  }

  getFavEvents(): Observable<EventFL[]>{
    return this.http
    .get<EventFL[]>("/api/user/me/visited", this.httpOptionsUser)
    .pipe(retry(1))
  }

  getStacks(){
    return this.http
    .get("/api/general/categories", this.httpOptionsDefault)
    .pipe(retry(1))
  }

  getCities(){
    return this.http
    .get("/api/general/cities", this.httpOptionsDefault)
    .pipe(retry(1))
  }

  postInfo(phone: string = '', first_name: string, last_name: string, status: any, city: any, stack: any){
    return this.http
    .post("/api/user/me",{
      phone: phone,
      first_name: first_name,
      last_name: last_name,
      status: status,
      city: city,
      stack: stack
    }, 
    this.httpOptionsUser)
  }

  postEmail(email: any, password: any){
    return this.http
    .post("/api/user/me/credentials",{
      email: email,
      old_password: password
    },
    this.httpOptionsUser)
  }

  postPassword(oldPass: any, newPass: any){
    console.log('hi')
    return this.http
    .post("/api/user/me/credentials",{
      old_password: oldPass,
      password: newPass,
    },
    this.httpOptionsUser)
  }

  getImg(imageUrl: string): Observable<Blob>{
    return this.http.get(imageUrl, {responseType: 'blob'})
  }

  uploadImage(image: File){
    const formData = new FormData();

    formData.append('avatar', image, image.name);

    return this.http
    .post('/api/user/me/avatar', formData, this.httpOptionsI)
  }
}
