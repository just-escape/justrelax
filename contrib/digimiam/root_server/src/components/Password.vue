<template>
  <div class="global-container glowing-container">
    <div class="d-flex flex-row justify-content-center align-items-center h-100">
      <div class="window position-relative">
        <div class="window-title py-1 px-2 w-100">PASSWORD</div>
        <div class="d-flex flex-column justify-content-between pt-5 pb-3 px-2 h-100">
          <div>
            Password, password, what's the password... today?
          </div>
          <div class="text-center">
            <div class="input-group">
              <input v-model="password" :type="inputType" class="form-control"/>
              <div class="input-group-append">
                <span
                  @mousedown="revealPassword"
                  @mouseup="hidePassword"
                  class="input-group-text"
                >
                  <i class="fas fa-eye"></i>
                </span>
              </div>
            </div>
          </div>
          <div class="text-right">
            <ButtonBlue @click="checkPassword">Unlock</ButtonBlue>
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
  border: 4px solid #00d1b6;
  border-top: 9px solid #00d1b6;
  box-shadow: 0px 0px 14px -6px rgba(0, 209, 182, 1);
}

.window-title {
  position: absolute;
  background-color: rgba(00, 45, 64, 0.6);
  border-bottom: 1px solid #00d1b6;
}

input {
  background: transparent;
  border-color: #00d1b6;
  color: #ffffff;
  border-radius: 0;
}

input:focus {
  box-shadow: 0 0 14px -6px rgba(0, 209, 182, 1);
  background-color: transparent;
  border-color: #00d1b6;
  color: #ffffff;
}

.input-group-text {
  background: transparent;
  border-color: #00d1b6;
  color: #00d1b6;
}
</style>
