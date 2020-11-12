import { retry } from 'rxjs/operators';
import { Stack } from './../../../models/stack';
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Router } from '@angular/router';
import { BehaviorSubject, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private isLoggedIn: BehaviorSubject<boolean>;

  httpOptions = {
    headers: new HttpHeaders({
      "Content-Type": "application/json; charset=utf-8"
    }),
  };

  httpPostOptions = {
    headers: new HttpHeaders({
      "Content-Type": "application/json; charset=utf-8"
    }),
    responseType: 'text'
  }

  constructor(private readonly http: HttpClient, private router: Router) { }

  login(username: string, password: string){
    console.log("logging in");
    

    return this.http
      .post("/api/user/login", {
        email: username,
        password: password
      }, {responseType: 'text'})
      
      
  }

  register(username: string, password: string, firstName: string, lastName: string, stack: any){
    console.log("signing up")

    return this.http
    .post("/api/user/register",{
      email: username,
      password: password,
      first_name: firstName,
      last_name: lastName,
      stack: stack
    }, {responseType: 'text'})
    
  }

  logout(){
    localStorage.removeItem("currentUser");
    this.router.navigate(["/"]);
    console.log(localStorage.getItem("currentUser"))
  }

  public get userIsLoggedIn(): boolean {
    return this.isLoggedIn.value;
  }

  getStacks(): Observable<Stack[]>{
    return this.http
<<<<<<< HEAD:frontend/WEB-client/src/app/modules/auth/services/auth.service.ts
    .get <Stack[]>('/api/general/stacks', this.httpOptions)
=======
    .get <Stack[]>('/api/general/categories', this.httpOptions)
>>>>>>> design:frontend/WEB-client/src/app/modules/auth/services/auth.service.ts
    .pipe(retry(1))
  }

  
}
