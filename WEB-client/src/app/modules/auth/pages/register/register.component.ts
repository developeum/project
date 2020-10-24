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
  registerForm: FormGroup;
  stacks: Stack[] = [];

  constructor(private formBuilder: FormBuilder, private router: Router, private authService: AuthService) { }

  @ViewChild("password") pass: ElementRef;

  ngOnInit(): void {
    this.loadStacks();
    this.registerForm = this.formBuilder.group({
      username: ["", Validators.required],
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
      x.forEach(stack => {
        this.stacks.push(stack)
      })
    })
  }

  onSubmit(){
    if (this.registerForm.invalid){
      console.log("form is invalid");
      return;
    }

    console.log(this.form.username, this.form.password)
    let stacks = [];
    stacks.push(this.stacks[this.form.stack.value])
    this.authService.register( this.form.username.value, this.form.password.value, this.form.firstName.value, this.form.lastName.value, stacks )
    this.router.navigate(['/'])
  }

}
