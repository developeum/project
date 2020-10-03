import { HomeComponent } from '../home/home.component';
import { HomeRoutingModule } from './home-routing.module';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HomeMainComponent } from './pages/home-main/home-main.component';



@NgModule({
    declarations: [
        HomeMainComponent,
        HomeComponent
    ],
    imports: [
        CommonModule,
        HomeRoutingModule,
    ]
})

export class HomeModule { }