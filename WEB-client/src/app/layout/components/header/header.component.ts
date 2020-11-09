import { Router } from '@angular/router';
import { Observable } from 'rxjs';
import { EventFL } from './../../../models/eventsFL';
import { HeaderService } from './../../service/header.service';
import { Component, OnInit, Output, EventEmitter, OnDestroy } from '@angular/core';

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
  searchVisibility: boolean = false;
  noEvents: boolean = false;

  @Output() onChanged = new EventEmitter<boolean>()

  change(){
    this.onChanged.emit(!this.searchVisibility)
  }

  constructor(private headerService: HeaderService, private router: Router) { 
    let reqInfo: {
      avatar: string;
      ok: boolean
    } 
    if(localStorage.getItem('currentUser') != null){
      this.userIsLoggedIn = true;
      this.headerService.getUserImgUrl().subscribe(x => {
        reqInfo = x;
        // console.log(reqInfo.avatar)
        this.loadImg(reqInfo.avatar)
      })
    }
  }

  createImgFromBlob(image: Blob){
    let reader = new FileReader();
    reader.addEventListener("load", () => {
      this.imageToShow = reader.result;
      // console.log(this.imageToShow)
    }, false);

    if (image) {
      // console.log("made")

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
    this.events$ = this.headerService.getSerchingEvents(name);
    this.events$.subscribe(x => {
      if(x.length == 0){
        this.noEvents = true;
      } else {
        this.noEvents = false
      }
    })
  }

  ngOnInit(): void {
  }

  navToEvent(id){
    this.router.navigateByUrl('/event/' + id)
  }

  searchEvents(event: any){
    if( event.target.value != ''){
      // console.log(event.target.value);
      this.loadSearchinEvents(event.target.value)
    } else {
      this.events$ = null
    }
    
  }

  changeSearchVisibility(){
    this.searchVisibility = !this.searchVisibility;
    this.change()
  }

}
