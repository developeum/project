import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { PersonalService } from './../../services/personal.service';
import { User } from './../../../../models/user';
import { Observable } from 'rxjs';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-user-info',
  templateUrl: './user-info.component.html',
  styleUrls: ['./user-info.component.scss']
})
export class UserInfoComponent implements OnInit {
  userInfoForm: FormGroup;
  currentUserId: string;
  base64Img: string;
  
  userInfo$: Observable<User>;
  userInfo = new User;

  visibility: boolean = false;
  invisibility: boolean = true;

  constructor(private pageService: PersonalService, private formBuilder: FormBuilder) { 
    
  }

  ngOnInit(): void {
    this.loadUserInfo();
    this.loadUserImg();
    this.userInfoForm = this.formBuilder.group({
      email: [this.userInfo.email, Validators.required],
      phone: [this.userInfo.phone, Validators.required],
      firstName: [this.userInfo.first_name, Validators.required],
      lastName: [this.userInfo.last_name, Validators.required],
    })
  }

  loadUserInfo(){
    this.pageService.getUserInfo().subscribe(x => this.processUserInfo(x))
  }

  processUserInfo(data: User){
    this.userInfo = data;
  }

  loadUserImg(){
    this.pageService.getPicBase64().subscribe(x => {
      this.base64Img = x.base64;
      console.log(this.base64Img)
    })
  }

  logout(){
    
  }

  changeVisibility(){
    this.visibility = !this.visibility;
    this.invisibility = !this.invisibility;
    console.log(this.visibility);
  }

}
