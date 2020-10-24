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

  constructor(private formBuilder: FormBuilder, private router: Router, private authService: AuthService) { }

  @ViewChild("password") pass: ElementRef;

  ngOnInit(): void {
    this.loginForm = this.formBuilder.group({
      username: [ "", Validators.required ],
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

  onSubmit(){
    if (this.loginForm.invalid){
      console.log("form is incorrect")
      return;
    }

    console.log(this.form.username, this.form.password)

    this.authService.login( this.form.username.value, this.form.password.value )
    this.router.navigate(['/'])
  }

}
