<template>
  <div>
    <q-separator spaced />
    <q-form
      dense
      @submit.prevent.stop="sendPerson"
     >
      <div class="row no-wrap">
         <div class="fit q-mr-xs">
          <q-input
            filled
            color="green-6"
            bg-color="green-1"
            class="q-mb-sm"
            v-model="person.first_name"
            label="* First name"
            lazy-rules
            :rules="[ val => val && val.length > 0 || 'Please type something']"
            hide-bottom-space
          />
          <q-input
            filled
            color="green-6"
            bg-color="green-1"
            class="q-mb-sm"
            v-model="person.middle_name"
            label="Middle name"
          />
          <q-input
            filled
            color="green-6"
            bg-color="green-1"
            class="q-mb-sm"
            v-model="person.last_name"
            label="* Last name"
            lazy-rules
            :rules="[ val => val && val.length > 0 || 'Please type something']"
            hide-bottom-space
          />
          <q-select
            filled
            options-cover
            color="green-6"
            class="q-mb-sm"
            v-model="person.person_gender.gender_name"
            bg-color="green-1"
            label="Person's gender"
            :display-value="CapitalizeFirstLetter(
              person.person_gender.gender_name
            )"
            :options="genderlist"
          />
        </div>
        <div class="fit q-ml-xs">
          <q-input
            filled
            unmasked-value
            mask="(###) ### - ####"
            color="green-6"
            bg-color="green-1"
            class="q-mb-sm"
            v-model="person.phone"
            label="Current telephone number"
          />
          <q-input
            filled
            color="green-6"
            bg-color="green-1"
            class="q-mb-sm"
            v-model="person.email"
            type="email"
            label="E-mail address"
            lazy-rules
          />
          <q-select
            filled
            color="green-6"
            bg-color="green-1"
            class="q-mb-sm"
            v-model="person.person_type.type_name"
            label="Person's operational type"
            options-cover
            :display-value="CapitalizeFirstLetter(
              person.person_type.type_name
            )"
            :options="typelist"
          />
          <q-input
            filled
            color="green-6"
            bg-color="green-1"
            class="q-mb-sm"
            v-model="person.birthday"
            label="Person's birthday"
          >
            <template v-slot:append>
              <q-icon
                name="event"
                color="green-6"
                class="cursor-pointer"
              >
                <q-popup-proxy
                  ref="qDateProxy"
                  transition-show="scale"
                  transition-hide="scale"
                >
                  <q-date
                    minimal
                    color="green-6"
                    description="Birthday"
                    mask="D/M/YYYY"
                    v-model="person.birthday"
                    @input="() => $refs.qDateProxy.hide()"
                  />
                </q-popup-proxy>
              </q-icon>
            </template>
          </q-input>
        </div>
      </div>
      <q-input
        filled
        autogrow
        color="green-6"
        bg-color="green-1"
        class="q-mb-sm"
        v-model="person.occupation"
        label="Person's current Occupation on the laboratory"
      />
      <q-input
        filled
        autogrow
        color="green-6"
        bg-color="green-1"
        class="q-mb-sm"
        v-model="person.institution"
        label="Person's current employing Institution"
      />

      <div class="flex row justify-center no-wrap q-mb-sm">
        <div class="flex row fit text-caption self-end content-end">
          Person data last modified: {{
              this.person.last_modified
            ? this.person.last_modified
            : "never"
          }}
        </div>
        <q-btn
          type="submit"
          class="bg-green-6 text-white"
        >
        <div v-show="!awaitingResponse">Submit</div>
        <div v-show="awaitingResponse">
          <q-spinner-oval
            color="green-8"
            size="sm"
          />
          </div>
        </q-btn>

      </div>
    </q-form>
    <q-separator />
  </div>
</template>


<script>
import {
  CapitalizeFirstLetter,
  DateToUnix,
  ParseDate,
} from '../../../utils/StringUtils';

export default {
  name: 'PersonEdit',

  props: {
    person: Object,
    types: Object,
    genders: Object,
  },

  data() {
    return {
      awaitingResponse: false,
      typelist: Object.keys(this.types),
      genderlist: Object.keys(this.genders),
    };
  },

  methods: {
    CapitalizeFirstLetter,
    DateToUnix,
    ParseDate,

    sendPerson() {
      this.awaitingResponse = true;
      const personData = {
        first_name: this.person.first_name,
        last_name: this.person.last_name,
        middle_name: this.person.middle_name,
        phone: this.person.phone,
        // email: this.person.email, // Requires backend implementation
        birthday: DateToUnix(this.person.birthday),
        occupation: this.person.occupation,
        institution: this.person.institution,
        type_id: this.types[this.person.person_type.type_name],
        gender_id: this.genders[this.person.person_gender.gender_name],
      };
      this.$axios.put(`personnel/${this.person.id}`, personData)
        .then((res) => {
          const successfulPostData = res.data;
          this.person.first_name = successfulPostData.first_name;
          this.person.last_name = successfulPostData.last_name;
          this.person.middle_name = successfulPostData.middle_name;
          this.person.phone = successfulPostData.phone;
          this.person.email = successfulPostData.email;
          this.person.birthday = ParseDate(successfulPostData.birthday);
          this.person.occupation = successfulPostData.occupation;
          this.person.institution = successfulPostData.institution;
          this.person.person_type = successfulPostData.person_type;
          this.person.person_gender = successfulPostData.person_gender;

          this.awaitingResponse = false;
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
};
</script>
