import { Stack } from './../../../../models/stack';
import { AuthService } from './../../services/auth.service';
import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss']
})
export class RegisterComponent implements OnInit {
  error: boolean = false;
  errorType: boolean = false;
  registerForm: FormGroup;
  stacks: Stack[] = [];

  constructor(private formBuilder: FormBuilder, private router: Router, private authService: AuthService) { }

  @ViewChild("password") pass: ElementRef;

  ngOnInit(): void {
    this.loadStacks();
    this.registerForm = this.formBuilder.group({
      username: ["", [Validators.required, Validators.email]],
      password: ["", Validators.required],
      firstName: ["", Validators.required],
      lastName: ["", Validators.required],
      stack: [1, Validators.required]
    });
  }

  get form(){
    return this.registerForm.controls;
  }

  changePassVisibility(i){
    if(this.pass.nativeElement.type === "password"){
      this.pass.nativeElement.type = "text";
    } else {
      this.pass.nativeElement.type = "password"
    }
  }

  loadStacks(){
    this.authService.getStacks()
    .subscribe(x => {
      this.stacks = x;
      console.log(this.stacks)
    })
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

  onSubmit(){
    if (this.registerForm.invalid){
      console.log("form is incorrect");
      this.error = true;
      this.errorType = false;
      return;
    }

    console.log(this.form.username, this.form.password)
    let stacks = [];
    stacks.push(this.form.stack.value)
    console.log(this.form.stack.value)
    this.authService.register( this.form.username.value, this.form.password.value, this.form.firstName.value, this.form.lastName.value, stacks )
    .subscribe((token) => {
      console.log(token);
      localStorage.removeItem("currentUser")
      localStorage.setItem("currentUser", token)
      this.router.navigate(['/'])
    },
    (error) => {
      this.error = true;
      this.error = true;
    })
    
  }

}
