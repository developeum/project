import { HeaderService } from './../../service/header.service';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent implements OnInit {
  imageToShow: any
  userIsLoggedIn: boolean = false;

  constructor(private headerService: HeaderService) { 
    if(localStorage.getItem('currentUser') != null){
      this.userIsLoggedIn = true;
      this.headerService.getUserImgUrl().subscribe(x => {
        this.loadImg(x)
      })
    }
  }

  createImgFromBlob(image: Blob){
    let reader = new FileReader();
    reader.addEventListener("load", () => {
      this.imageToShow = reader.result;
      console.log(this.imageToShow)
    }, false);

    if (image) {
      console.log("made")

      reader.readAsDataURL(image)
    }
  }

  loadImg(url: string){
    this.headerService.getImg(url).subscribe(data => {
      this.createImgFromBlob(data);
    }, error => {
      console.log(error);
      console.log("error")
    });
  }

  ngOnInit(): void {
  }

}
