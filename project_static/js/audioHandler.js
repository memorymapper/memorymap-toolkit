let audioHandler = {
    
    sounds: {},

    formatTime: function(secs) {
        let minutes = Math.floor(secs / 60) || 0;
        let seconds = (secs - minutes * 60) || 0;
        return minutes + ':' + (seconds < 10 ? '0' : '') + seconds;
    },

    step: function(secs) {
        // Loop over the sounds and update the player progress bars on those which are playing
        for (let key in audioHandler.sounds) {
            let seek = audioHandler.sounds[key].seek() || 0;
            let time = audioHandler.formatTime(Math.round(seek));
            let duration = audioHandler.sounds[key].duration();
            let progress_bar_length = (seek/duration) * 100;
            $('.' + key + ' .progress_bar_fill').css('width', progress_bar_length + '%');
            $('.' + key + ' .player_timer').html(time);
            if (audioHandler.sounds[key].playing()) {
                requestAnimationFrame(audioHandler.step);
            }
        }
    },

    handleAudio: function(file, title, playerId) {
        // First, pause all the other sounds
        for (let key in this.sounds) {
            if (key != playerId) {
                try {
                    if (this.sounds[key].playing()) {
                        this.sounds[key].pause();
                        $('.' + key + ' .play_button').attr('src', '/static/img/play.svg');
                    }
                } catch (err) {
                    // Do nothing if no other sounds exit
                };
            }
        }

        // Then, if there are more than 5 sounds loaded, unload and delete the first so there are never more than 5 sounds loaded in memory.
        let soundsKeys = Object.keys(this.sounds);
        if (soundsKeys.length > 5) {
            let firstSound = soundsKeys[0];
            this.sounds[firstSound].unload();
            delete this.sounds[firstSound];
        }

        // Then check if the passed sound exists, and if so, pause it if it's playing and play it if it's paused
        try {
            if (this.sounds[playerId].playing()) {
                this.sounds[playerId].pause();
                $('.' + playerId + ' .play_button').attr('src', '/static/img/play.svg');
            } else {
                this.sounds[playerId].play();
                $('.' + playerId + ' .play_button').attr('src', '/static/img/pause.svg');
            }
        } catch {
            // Otherwise, set up a new sound and start playing it
            this.sounds[playerId] = new Howl({
                src: [file],
                html5: true,
                onplay: function() {
                    requestAnimationFrame(audioHandler.step);
                }
            });
            this.sounds[playerId].play();
            $('.' + playerId + ' .play_button').attr('src', '/static/img/pause.svg');
        }   
    },

    setSeekPositionFromProgressBar: function(playerId, percentage) {
        try {
            let one_percent = this.sounds[playerId].duration() / 100;
            let seek_value = one_percent * percentage;
            this.sounds[playerId].seek(seek_value);
            let seek = this.sounds[playerId].seek() || 0;
            let time = audioHandler.formatTime(Math.round(seek));
            $('.' + playerId + ' .progress_bar_fill').css('width', percentage + '%');
            $('.' + playerId + ' .player_timer').html(time);
        } catch(err) {
            console.log(err);
        }
    },

    updateProgressBar: function(playerId) {
        // Update the progress bar width (if a sound has previously been played)
        try {
            var seek = this.sounds[playerId].seek() || 0;
            var time = audioHandler.formatTime(Math.round(seek));
            var duration = this.sounds[playerId].duration();
            var progress_bar_length = (seek/duration) * 100;
            $('.' + playerId + ' .progress_bar_fill').css('width', progress_bar_length + '%');
            $('.' + playerId + ' .player_timer').html(time);
        } catch(err) {
            // do nothing
        }
    }
}