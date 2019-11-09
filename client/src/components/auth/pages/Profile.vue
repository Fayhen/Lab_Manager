<template>
  <q-page class="flex flex-center">
    <div class="main-form-container">

      <q-form @submit.prevent.stop="postData()"
        class="fit column wrap justify-center">
        <div>

          <!-- Upper buttons div -->
          <div class="q-mb-sm column text-center">
            <q-tooltip v-model="tip"
              class="q-pt-sm q-pb-sm q-pl-lg q-pr-lg q-mb-sm
                bg-green-3 rounded-borders custom-tooltip">
              <q-icon name="info" color="green-10" size="0.95em"/>
              You seen to have not updated your personal data yet.
              You may do so by clicking on the "edit" button.
            </q-tooltip>
            <div class="row justify-end">
              <q-btn outline
                label="Change picture"
                color="green-6"
                />
              <q-btn outline
                label="Edit information"
                color="green-6" class="q-ml-sm"
                @click="disabled = !disabled"
                />
            </div>
          </div>
          <!-- Close upper buttons div -->

          <!-- Image and fields div -->
          <div class="row">
            <div class="q-mr-sm col-auto img-container gibe-border">
              <img src="https://cdn.quasar.dev/img/parallax2.jpg">
            </div>
            <div class="col-grow">
              <q-input stack-label :readonly="disabled"
                ref="fullname"
                label="Full name"
                v-model="fullname"
                placeholder="Your full name"
                color="green-6"
                />
              <q-input stack-label :readonly="disabled"
                ref="email"
                label="Email"
                type="email"
                v-model="email"
                placeholder="youremail@email.com"
                color="green-6"
                :rules="[val => !!val || 'This field is required']"
                />
              <q-input stack-label :readonly="disabled"
                ref="username"
                label="Username"
                v-model="username"
                placeholder="Your username"
                color="green-6"
                :rules="[val => !!val || 'This field is required']"
                />
            </div>
          </div>
          <!-- Close Image and fields div -->

          <!-- Phone and birthday div -->
          <div class="row justify-between">
            <q-input stack-label :readonly="disabled"
              ref="phone"
              label="Phone number"
              v-model="phone"
              placeholder="Your phone number"
              color="green-6" class="col-grow"
              />
            <q-input stack-label :readonly="disabled"
              ref="birthday"
              label="Birthday"
              type="date"
              v-model="birthday"
              color="green-6" class="q-ml-sm col-5"
              />
          </div>
          <!-- Close Phone and birthday div -->

          <q-input stack-label :readonly="disabled"
            ref="institution"
            label="Institution"
            v-model="institution"
            placeholder="The institution you currently belong to"
            color="green-6"
            />
          <q-input stack-label :readonly="disabled"
            ref="occupation"
            label="Occuptation"
            type="textarea"
            v-model="occupation"
            placeholder="Your current occupation. E.g. Dept. Head, Tenured teacher"
            color="green-6"
            />
          <q-input stack-label :readonly="disabled"
            ref="function"
            label="Function"
            type="textarea"
            v-model="personType"
            placeholder="Your role at the laboratory. E.g. Researcher, Field Technician"
            color="green-6"
            />
        </div>
      </q-form>
    </div>
  </q-page>
</template>

<script>
import { update } from '../../../store/state.js';

export default {
  name: 'Profile',
  data() {
    return {
      email: '',
      username: '',
      fullname: '',
      firstname: '',
      middlename: '',
      lastname: '',
      phone: '',
      birthday: '',
      occupation: '',
      institution: '',
      personType: '',
      gender: '',
      frequency: [],
      fieldEvents: [],
      notices: [],
      disabled: true,
      tip: false,
    };
  },
  mounted() {
    update('Profile component on Auth module.');
    this.getData();
  },
  methods: {
    parseName(firstname, middlename, lastname) {
      const names = (middlename === '')
        ? [firstname, lastname]
        : [firstname, middlename, lastname];
      this.fullname = names.join(' ');
    },
    getData() {
      this.$axios.get('/auth/profile')
        .then((res) => {
          this.email = res.data.email;
          this.username = res.data.username;
          this.notices = res.data.notices;
          if (res.data.person_id) {
            this.firstname = res.data.person_id.first_name;
            this.middlename = (res.data.person_id.middle_name)
              ? res.data.person_id.middle_name
              : '';
            this.lastname = res.data.person_id.last_name;
            this.phone = res.data.person_id.phone;
            this.birthday = res.data.person_id.birthday;
            this.occupation = res.data.person_id.occupation;
            this.institution = res.data.person_id.institution;
            this.personType = res.data.person_id.type_id;
            this.gender = res.data.person_id.gender_id;
            this.frequency = res.data.person_id.frequency;
            this.parseName(this.first_name, this.middlename, this.lastname);
          } else {
            this.tip = true;
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
    postData() {
      console.log('WIP...');
    },
  },
};
</script>

<style lang="stylus" scoped>
  img
    max-width 100%
    max-height 100%
    border-radius 50%
  .img-container
    max-width 190px
    max-height 190px
</style>
