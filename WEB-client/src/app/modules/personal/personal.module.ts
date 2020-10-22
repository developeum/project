import { ReactiveFormsModule } from '@angular/forms';
import { GeneralModule } from './../../layout/components/general.module';
import { PersonalRoutingModule } from './personal-routing.module';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PersonalMainComponent } from './pages/personal-main/personal-main.component';
import { UserInfoComponent } from './components/user-info/user-info.component';
import { FavEventsComponent } from './components/fav-events/fav-events.component';



@NgModule({
  declarations: [
    PersonalMainComponent,
    UserInfoComponent,
    FavEventsComponent
  ],
  imports: [
    CommonModule,
    PersonalRoutingModule,
    GeneralModule,
    ReactiveFormsModule
  ]
})
export class PersonalModule { }
