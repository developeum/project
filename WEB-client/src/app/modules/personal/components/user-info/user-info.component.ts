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
  stacks: any;
  
  userInfo$: Observable<User>;
  userInfo = new User;

  visibility: boolean = false;

  statuses: any = [
    {
      id: 1,
      name: "student",
    },
    {
      id: 2,
      name: "worker",
    },
    {
      id: 3,
      name: "other"
    }
  ]

  constructor(private pageService: PersonalService, private formBuilder: FormBuilder) { 
    
  }

  ngOnInit(): void {
    this.loadUserInfo();
    this.loadUserImg();
    this.loadStacks();
    this.userInfoForm = this.formBuilder.group({
      phone: [this.userInfo.phone, Validators.required],
      firstName: [this.userInfo.first_name, Validators.required],
      lastName: [this.userInfo.last_name, Validators.required],
      stack: [this.userInfo.stack[0].name, Validators.required],
      status: [this.userInfo.status.name, Validators.required],
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

  loadStacks(){
    this.pageService.getStacks().subscribe(x => {
      this.stacks = x;
    })
  }

  logout(){
    
  }

  changeVisibility(){
    this.visibility = !this.visibility;
    console.log(this.visibility);
  }

  onSubmit(){
    this.pageService.postInfo(this.userInfo)
    .subscribe(() => {
      console.log("userInfoPushed");
      this.loadUserInfo()
      this.visibility = !this.visibility;
    })
  }

}
