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
    })
  };

  constructor(private readonly http: HttpClient, private router: Router) { }

  login(username: string, password: string){
    console.log("logging in");
    

    return this.http
      .post<string>("http://localhost:8000/api/user/login", {
        email: username,
        password: password
      })
      .subscribe((token) => {
        console.log(token);
        localStorage.removeItem("currentUser")
        localStorage.setItem("currentUser", token);
        console.log(localStorage.getItem("currentUser"))
      })
  }

  register(username: string, password: string, firstName: string, lastName: string, stack: Stack[]){
    console.log("signing up")

    return this.http
    .post<string>("http://localhost:8000/api/user/register",{
      username,
      password,
      firstName,
      lastName,
      stack
    })
    .subscribe((token) => {
      console.log(token);

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
