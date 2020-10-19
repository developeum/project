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
  currentUserId: string;
  base64Img: string;
  
  userInfo$: Observable<User>;
  userInfo = new User;


  constructor(private pageService: PersonalService) { }

  ngOnInit(): void {
    this.loadUserInfo();
    this.loadUserImg();
  }

  loadUserInfo(){
    this.pageService.getUserInfo().subscribe(x => this.processUserInfo(x))
  }

  processUserInfo(data: User){
    this.userInfo = data;
  }

  loadUserImg(){
    this.pageService.getPicBase64(this.currentUserId).subscribe(x => {
      this.base64Img = x.base64;
      console.log(this.base64Img)
    })
  }

  logout(){
    
  }

}
