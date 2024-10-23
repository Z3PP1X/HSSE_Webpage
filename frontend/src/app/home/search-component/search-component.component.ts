import { Component } from '@angular/core';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { HeaderComponent } from '../header/header.component';
import { MatSidenavModule } from '@angular/material/sidenav';


@Component({
  selector: 'app-search-component',
  standalone: true,
  imports: [MatButtonModule, MatInputModule, MatIconModule, MatCardModule, HeaderComponent, MatSidenavModule],
  templateUrl: './search-component.component.html',
  styleUrl: './search-component.component.scss'
})
export class SearchComponentComponent {

}
