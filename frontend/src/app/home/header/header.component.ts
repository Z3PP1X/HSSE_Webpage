import { Component, output} from '@angular/core';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { UserComponent } from '../user/user.component';
import { Injectable } from '@angular/core';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';



@Component({
  selector: 'app-header',
  standalone: true,
  imports: [
    MatToolbarModule,
    MatButtonModule,
    MatIconModule,
    UserComponent,
    RouterOutlet,
    RouterLink,
    RouterLinkActive,
  ],
  providers: [],
  templateUrl: './header.component.html',
  styleUrl: './header.component.css',
})
export class HeaderComponent {

  toggleSidenav = output<boolean>();

  public IncidentRecord = "/ehs";

  ontoggleSidenav() {
    this.toggleSidenav.emit(true);
    console.log("Sidebar event triggered")
  }
}
