import { Router } from '@angular/router';
import { City } from './../../../../models/city';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { PersonalService } from './../../services/personal.service';
import { User } from './../../../../models/user';
import { Observable } from 'rxjs';
import { Component, OnInit } from '@angular/core';

class ImageSnippet {
  constructor(public src: string, public file: File) {}
}

@Component({
  selector: 'app-user-info',
  templateUrl: './user-info.component.html',
  styleUrls: ['./user-info.component.scss']
})
export class UserInfoComponent implements OnInit {
  changeMod: boolean = false;
  imageToShow: any;
  userInfoForm: FormGroup;
  loginForm: FormGroup;
  passwordForm: FormGroup;
  currentUserId: string;
  stacks: any;
  cities: any;
  

  selectedFile: ImageSnippet;
  
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

  constructor(private pageService: PersonalService, private formBuilder: FormBuilder, private router: Router) { 
    
  }

  ngOnInit(): void {
    this.loadUserInfo();
    this.loadStacks();
    this.loadCities();
    this.createChangeLogPassForms();
  }

  loadUserInfo(){
    this.pageService.getUserInfo().subscribe(x => this.processUserInfo(x))
  }

  processUserInfo(data: any){
    this.userInfo$ = this.pageService.getUserInfo();
    this.userInfo = data;
    this.userInfoForm = this.formBuilder.group({
      phone: [this.userInfo.phone, Validators.required],
      firstName: [this.userInfo.first_name, Validators.required],
      lastName: [this.userInfo.last_name, Validators.required],
      stack: [this.userInfo.stack[0].id, Validators.required],
      status: [this.userInfo.status.id, Validators.required],
      city: [this.userInfo.city.id, Validators.required],
    });
    if(data.profile_img != null){
      this.loadImg(data.profile_img);
    }
  }

  createChangeLogPassForms(){
    this.loginForm = this.formBuilder.group({
      login: ["", Validators.required],
      password: ["", Validators.required]
    });
    this.passwordForm = this.formBuilder.group({
      oldPass: ["", Validators.required],
      password: ["", Validators.required]
    })
  }

  loadStacks(){
    this.pageService.getStacks().subscribe(x => {
      this.stacks = x;
    })
  }

  loadCities(){
    this.pageService.getCities().subscribe(x => {
      this.cities = x;
    })
  }

  get form(){
    return this.userInfoForm.controls;
  }

  get logForm(){
    return this.loginForm.controls;
  }

  get passForm(){
    return this.passwordForm.controls;
  }

  logout(){
    localStorage.removeItem('currentUser')
    this.router.navigateByUrl('/');
    console.log('error')
  }

  changeVisibility(){
    this.visibility = !this.visibility;
    console.log(this.visibility);
    this.changeMod = true;
  }

  onSubmit(){
    let currentStack = [];
    currentStack.push(this.form.stack.value)
    console.log("begin")
    this.pageService.postInfo(this.form.phone.value, this.form.firstName.value, this.form.lastName.value, this.form.status.value, this.form.city.value, currentStack)
    .subscribe(() => {
      console.log("userInfoPushed");
      console.log(this.form.phone.value, this.form.firstName.value, this.form.lastName.value, this.form.status.value, this.form.city.value, this.form.stack.value)
      this.loadUserInfo()
      this.visibility = !this.visibility;
      this.changeMod = false;
    })
  }

  createImgFromBlob(image: Blob){
    let reader = new FileReader();
    reader.addEventListener("load", () => {
      this.imageToShow = reader.result;
    }, false);

    if (image) {
      console.log("made")

      reader.readAsDataURL(image)
    }
  }

  loadImg(url: string){
    this.pageService.getImg(url).subscribe(data => {
      this.createImgFromBlob(data);
    }, error => {
      console.log(error);
      console.log("error")
    });
  }

  processFile(imageInput: any){
    const file: File = imageInput.files[0];
    const reader = new FileReader();

    reader.addEventListener('load', (event: any) => {

      this.selectedFile = new ImageSnippet(event.target.result, file);

      this.pageService.uploadImage(this.selectedFile.file).subscribe(
        (res) => {
          console.log(res);
          console.log("successfully upload");
          this.imageToShow = this.selectedFile.src
        },
        (err) => {
          console.log(err);
          console.log("error")
        })
    });

    

    reader.readAsDataURL(file);
  }

  changeEmail(){
    console.log(this.logForm.login.value)
    this.pageService.postEmail(this.logForm.login.value, this.logForm.password.value).subscribe(x => {
      console.log(x)
      this.loadUserInfo();
    })
  }

  changePass(){
    this.pageService.postPassword(this.passForm.oldPass.value, this.passForm.password.value).subscribe(x => {
      console.log(x)
    })
  }

}
