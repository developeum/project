import { AuthService } from './../../services/auth.service';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss']
})
export class RegisterComponent implements OnInit {
  registerForm: FormGroup;

  constructor(private formBuilder: FormBuilder, private router: Router, private authService: AuthService) { }

  ngOnInit(): void {
    this.registerForm = this.formBuilder.group({
      username: ["", Validators.required],
      password: ["", Validators.required]
    });
  }

  get form(){
    return this.registerForm.controls;
  }

  onSubmit(){
    if (this.registerForm.invalid){
      console.log("form is invalid");
      return;
    }

    console.log(this.form.username, this.form.password)

    this.authService.register( this.form.username.value, this.form.password.value )
    this.router.navigate(['/'])
  }

}
