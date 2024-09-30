import { Component, output} from '@angular/core';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { UserComponent } from '../user/user.component';
import { Injectable} from '@angular/core';


@Component({
  selector: 'app-header',
  standalone: true,
  imports: [
    MatToolbarModule,
    MatButtonModule,
    MatIconModule,
    UserComponent,
  ],
  providers: [],
  templateUrl: './header.component.html',
  styleUrl: './header.component.scss',
})
export class HeaderComponent {

  toggleSidenav = output<boolean>(); 

  ontoggleSidenav() {
    this.toggleSidenav.emit(true);
    console.log("Sidebar event triggered")
  }

}
