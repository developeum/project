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
  imageToShow: any;
  userInfoForm: FormGroup;
  currentUserId: string;
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
    this.loadImg(data.profile_img);
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

  createImgFromBlob(image: Blob){
    let reader = new FileReader();
    reader.addEventListener("load", () => {
      this.imageToShow = reader.result;
    }, false);

    if (image) {
      reader.readAsDataURL(image)
    }
  }

  loadImg(url: string){
    this.pageService.getImg(url).subscribe(data => {
      this.createImgFromBlob(data);
    }, error => {
      console.log(error);
    });
  }

}
