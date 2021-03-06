import {
    HttpInterceptor,
    HttpRequest,
    HttpHandler,
    HttpEvent,
    HTTP_INTERCEPTORS
  } from "@angular/common/http";
  import { AuthService } from "../services/auth.service";
  import { Observable } from "rxjs";
  import { Injectable } from "@angular/core";
  
  @Injectable({
    providedIn: "root"
  })
  export class JwtInterceptor implements HttpInterceptor {
    constructor(private authenticationService: AuthService) {}
  
    intercept(
      request: HttpRequest<any>,
      next: HttpHandler
    ): Observable<HttpEvent<any>> {
      // add authorization header with jwt token if available
      
      
      request = request.clone({
        setHeaders: {
          'X-Session-Token': `${localStorage.getItem("currentUser")}`
        }
      });
      
  
      return next.handle(request);
    }
  }
  
  export const jwtInterceptorProvider = {
    provide: HTTP_INTERCEPTORS,
    useClass: JwtInterceptor,
    multi: true
  };