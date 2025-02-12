import type { Schema, Struct } from '@strapi/strapi';

export interface SafetyAlarmplan extends Struct.ComponentSchema {
  collectionName: 'components_safety_alarmplans';
  info: {
    description: '';
    displayName: 'Alarmplan';
    icon: 'archive';
  };
  attributes: {
    Logo: Schema.Attribute.Media<'images' | 'files'> &
      Schema.Attribute.Required;
    Titel: Schema.Attribute.String & Schema.Attribute.Required;
  };
}

export interface SafetyUnfall extends Struct.ComponentSchema {
  collectionName: 'components_safety_unfalls';
  info: {
    description: '';
    displayName: 'Unfall';
  };
  attributes: {
    KatContent: Schema.Attribute.Blocks & Schema.Attribute.Required;
    KatIcon: Schema.Attribute.Media<'images' | 'files', true> &
      Schema.Attribute.Required;
    KatSubtitle: Schema.Attribute.String &
      Schema.Attribute.Required &
      Schema.Attribute.DefaultTo<'RUHE BEWAHREN!'>;
    Titel: Schema.Attribute.String &
      Schema.Attribute.Required &
      Schema.Attribute.DefaultTo<'Verhalten bei Unf\u00E4llen'>;
  };
}

declare module '@strapi/strapi' {
  export module Public {
    export interface ComponentSchemas {
      'safety.alarmplan': SafetyAlarmplan;
      'safety.unfall': SafetyUnfall;
    }
  }
}
