import { AuthRoutingModule } from './auth-routing.module';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LoginComponent } from './pages/login/login.component'

@NgModule({
    declarations: [LoginComponent],
    imports: [
        CommonModule,
        AuthRoutingModule
    ]
})

export class AuthModule { }