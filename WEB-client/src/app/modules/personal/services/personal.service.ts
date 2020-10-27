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

  httpOptionsUser = {
    headers:{
      "Content-Type": "multipart/form-data",
      "X-Session-Token": `${this.getToken}`
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
    console.log('getting')
    return this.http
    .get<User>("http://localhost:8000/api/user/me", this.httpOptionsUser)
    .pipe(retry(1))
  }

  getFavEvents(): Observable<EventFL[]>{
    return this.http
    .get<EventFL[]>("http://localhost:8000/api/user/me/visited", this.httpOptionsUser)
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
    }, 
    this.httpOptionsUser)
  }

  getImg(imageUrl: string): Observable<Blob>{
    return this.http.get(imageUrl, {responseType: 'blob'})
  }

  uploadImage(image: File){
    const formData = new FormData();

    formData.append('image', image);

    return this.http
    .post('http://localhost:8000/api/user/me/avatar', {avatar: formData}, this.httpOptionsUser)
  }
}
