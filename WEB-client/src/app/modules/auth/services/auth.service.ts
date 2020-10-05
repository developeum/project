import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private isLoggedIn: BehaviorSubject<boolean>;

  constructor(private readonly http: HttpClient, private router: Router) { }

  login(username: string, password: string){
    console.log("logging in");
    

    return this.http
      .post<string>("http://localhost:8000/api/identity/login", {
        username,
        password
      })
      .subscribe((token) => {
        console.log(token);

        localStorage.setItem("currentUser", token);
      })
  }

  register(username: string, password: string){
    console.log("signing up")

    return this.http
    .post<string>("http://localhost:8000/api/identity/register",{
      username,
      password
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
}
