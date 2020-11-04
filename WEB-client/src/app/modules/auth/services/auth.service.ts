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
      .post("http://localhost:8000/api/user/login", {
        email: username,
        password: password
      }, {responseType: 'text'})
      
      
  }

  register(username: string, password: string, firstName: string, lastName: string, stack: any){
    console.log("signing up")

    return this.http
    .post("http://localhost:8000/api/user/register",{
      email: username,
      password: password,
      first_name: firstName,
      last_name: lastName,
      stack: stack
    }, {responseType: 'text'})
    .subscribe((token) => {
      console.log(token);
      localStorage.removeItem("currentUser")
      localStorage.setItem("currentUser", token)
    })
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
    .get <Stack[]>('http://localhost:8000/api/general/stacks', this.httpOptions)
    .pipe(retry(1))
  }

  
}
