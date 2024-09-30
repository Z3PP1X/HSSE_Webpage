import { Component, input } from '@angular/core';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { SubmittableForm } from './SubmittableForm.model';


@Component({
  selector: 'app-submittable-form-card',
  standalone: true,
  imports: [MatCardModule, MatFormFieldModule, MatInputModule, MatButtonModule],
  templateUrl: './submittable-form-card.component.html',
  styleUrl: './submittable-form-card.component.scss',
})
export class SubmittableFormCardComponent {
  dataModel = input.required<SubmittableForm[]>();
}
