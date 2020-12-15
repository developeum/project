import { AuthService } from './../../services/auth.service';
import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';


@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {
  loginForm: FormGroup;
  error: boolean = false;
  errorType: boolean = false; //errorType = false - тип ошибки(некорректные данные)

  constructor(private formBuilder: FormBuilder, private router: Router, private authService: AuthService) { }

  @ViewChild("password") pass: ElementRef;

  ngOnInit(): void {
    this.loginForm = this.formBuilder.group({
      username: [ "", [ Validators.required, Validators.email ] ],
      password: [ "", Validators.required ]
    });
  }

  get form() {
    return this.loginForm.controls;
  }

  changePassVisibility(i){
    if(this.pass.nativeElement.type === "password"){
      this.pass.nativeElement.type = "text";
    } else {
      this.pass.nativeElement.type = "password"
    }
  }

  fixForm(){
    // if( this.loginForm.invalid ){
    //   this.error = true;
    //   return;
    // }
    this.error = false;
    this.errorType = false;
    console.log("form changed")
  }

  makeNoError(){
    this.error = false;
  }

  onSubmit(){
    if (this.loginForm.invalid){
      console.log("form is incorrect");
      this.error = true;
      this.errorType = false;
      return;
    }

    console.log(this.form.username.value, this.form.password.value)
    this.authService.login( this.form.username.value, this.form.password.value )
    .subscribe(token => {
      if(token.length <= 60){
        this.error = true;
        this.errorType = true;
        return
      }
      localStorage.removeItem("currentUser")
      localStorage.setItem("currentUser", token);
      this.router.navigate(['/'])
    })
    
  }

}
