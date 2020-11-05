import { Router } from '@angular/router';
import { Observable } from 'rxjs';
import { EventFL } from './../../../models/eventsFL';
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
  events$: Observable<EventFL[]>;
  searchParam: string = '';

  constructor(private headerService: HeaderService, private router: Router) { 
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

  loadSearchinEvents(name: string){
    this.events$ = this.headerService.getSerchingEvents(name)
  }

  ngOnInit(): void {
  }

  navToEvent(id){
    this.router.navigateByUrl('/event/' + id)
  }

  searchEvents(event: any){
    console.log(event.target.value);
    this.loadSearchinEvents(event.target.value)
  }

}
