import { Component, signal } from '@angular/core';
import { DUMMY_USERS } from '../dummy-user';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';

const randomIndex = Math.floor(Math.random() * DUMMY_USERS.length);

@Component({
  selector: 'app-user',
  standalone: true,
  imports: [MatButtonModule, MatIconModule],
  templateUrl: './user.component.html',
  styleUrl: './user.component.scss'
})
export class UserComponent {

  loggedInUser = signal(DUMMY_USERS[randomIndex]);


  changeUser() {
    const randomIndex = Math.floor(Math.random() * DUMMY_USERS.length);
    this.loggedInUser.set(DUMMY_USERS[randomIndex]);
  }

  

}
