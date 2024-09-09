import { Component, signal } from '@angular/core';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { UserComponent } from '../user/user.component';
import { SidebarComponent } from '../sidebar/sidebar.component';
import { SidebarService } from '../services/sidebar.service';
import { Injectable} from '@angular/core';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [
    MatToolbarModule,
    MatButtonModule,
    MatIconModule,
    UserComponent,
    SidebarComponent,
  ],
  providers: [SidebarService, Injectable],
  templateUrl: './header.component.html',
  styleUrl: './header.component.scss',
})
export class HeaderComponent {
  constructor(public sidebarService: SidebarService) {}
}
