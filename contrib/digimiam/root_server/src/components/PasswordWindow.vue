<template>
  <div class="global-container glowing-container">
    <div class="d-flex flex-row justify-content-center align-items-center h-100">
      <div class="window position-relative">
        <div class="window-title py-1 px-2 w-100">{{ $t('password') }}</div>
        <div class="d-flex flex-column justify-content-between pt-5 pb-3 px-2 h-100">
          <div>
            {{ $t('this_operation_requires_a_password') }}
          </div>
          <div class="text-center position-relative">
            <input v-model="password" :type="inputType" class="form-control pr-34px"/>
            <div
              @mousedown="revealPassword"
              @mouseup="hidePassword"
              class="position-absolute d-flex align-items-center eye"
            >
              <i class="px-2 fas fa-eye"></i>
            </div>
          </div>
          <div class="text-right">
            <ButtonBlue @click="checkPassword">{{ $t('continue') }}</ButtonBlue>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ButtonBlue from '@/components/ButtonBlue.vue'

export default {
  name: 'Password',
  components: {
    ButtonBlue
  },
  data: function() {
    return {
      password: '',
      inputType: 'password',
    }
  },
  methods: {
    revealPassword: function() {
      this.inputType = 'text'
    },
    hidePassword: function() {
      this.inputType = 'password'
    },
    checkPassword: function() {
      var event
      if (this.password == 'password') {
        event = JSON.stringify(
          {
            "type": "MSG",
            "content": "password_ok",
          }
        )
      } else {
        event = JSON.stringify(
          {
            "type": "MSG",
            "content": "password_ko",
          }
        )
      }
      this.$socket.send(event)
    }
  },
}
</script>

<style scoped>
.window {
  width: 600px;
  height: 300px;
  border: 4px solid orangered;
  border-top: 9px solid orangered;
  box-shadow: 0px 0px 14px -6px rgba(255, 69, 0, 1);
  background-color: rgba(0, 0, 0, 0.2);
  color: #fd7e14;
}

.window-title {
  color: orangered;
  position: absolute;
  background-color: rgba(0, 0, 0, 0.5);
  border-bottom: 1px solid orangered;
}

input {
  background: transparent;
  border-color: #fd7e14;
  color: #fd7e14;
}

input:focus {
  box-shadow: 0 0 14px -6px rgba(255, 69, 0, 1);
  background-color: transparent;
  border-color: #fd7e14;
  color: #ffffff;
}

.pr-34px {
  padding-right: 34px;
}

.eye {
  right: 0;
  top: 0;
  bottom: 0;
  color: #fd7e14;
}
</style>
